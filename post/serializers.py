from rest_framework import serializers

from post.models import Company as CompanyModel
from post.models import JobPost as JobPostModel
from post.models import JobType as JobTypeModel
from post.models import SkillSet as SkillSetModel
from post.models import JobPostSkillSet as JobPostSkillSetModel
from post.models import CompanyBusinessArea as CompanyBusinessAreaModel
from post.models import BusinessArea as BusinessAreaModel

# 1. Company Serializer (model = Company) 구현**
# 2. JobPost Serializer (model = JobPost) 구현**
# 3. JobPostSkillSet Serializer (model = JobPostSkillSet) 구현**

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = ["id", "company_name"]


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTypeModel
        fields = ["job_type"]


class BusinessAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAreaModel
        fields = ["area"]


class JobPostSerializer(serializers.ModelSerializer):
    # job_type = JobTypeSerializer()
    company = CompanySerializer()

    skillsets = serializers.SerializerMethodField()
    def get_skillsets(self, obj):
        # obj : 불러온 JobPostModel
        # jobpostskillset : JobPostSkillSet 모델에 연관되어 있는 job_post 역참조
        # JobPost 모델에는 JobPostSkillSet를 찾을 수 없기에 _set을 붙여 역참조를 가능하게 했다.
        return [skill.skill_set.name for skill in obj.jobpostskillset_set.all()]

    job_type = serializers.SerializerMethodField()
    def get_job_type(self, obj):
        # obj : 불러온 JobPostModel
        # 1)job_type : JobPostModel 안에 있는 job_type
        # 2)job_type : ForeignKey로 연결된 JobTypeModel 안에 있는 job_type (역참조)
        type_name = obj.job_type.job_type
        return type_name

    class Meta:
        model = JobPostModel
        fields = ["id", "job_type", "company", "job_description", "salary", "skillsets"]

    def create(self, validated_data):
        # validated_data = {
        # "job_type": {"job_type": "permanent", "job_type": "temporary"}, 
        # "company" : {"company_name" : "company1", "company_name" : "company2" ~} ~}

        # 입력받은 validated_data 안에 있는 job_type query를 찾는다. (JobPost 모델에서)
        # {"job_type": "permanent", "job_type": "temporary"}
        # 만약 permanent를 입력받았으면 {"job_type": "permanent"} 하나만
        job_type_data = validated_data.pop("job_type")

        # 찾은 job_type query에서 job_type라는 이름 데이터를 찾는다. (JobType 모델에서)
        # {"permanent", "temporary"}
        # 만약 permanent를 입력받았으면 {"permanent"} 하나만
        job_type_name = job_type_data.get("job_type")

        # 찾은 이름 데이터를 JobType 모델에서 object로 찾는다.
        # 만약 permanent를 입력받았으면 해당 데이터와 같은 object를 넣어준다.
        job_type_obj = JobTypeModel.objects.get(job_type=job_type_name)
        # → 하지만 이 부분은 views.py에서 작성을 했??


        # 이후 company도 마찬가지
        company_data = validated_data.pop("company") # JobPost 모델에서 찾는다.
        company_name = company_data.get("company_name") # Company 모델에서 찾는다.

        company_obj = CompanyModel.objects.get(company_name=company_name)
        # → 하지만 이 부분은 views.py에서 작성을 했??

        # 찾은 object들을 JobPost 모델에서 해당하는 필드(job_type, company)에 넣어준다.
        # 다른 값들은 입력받은 값 그대로 넣어준다. (**validated_data)
        # = 왜? 입력받은 값은 serializer를 거쳐서 object로 반환되기 때문이다.
        post_data = JobPostModel(job_type=job_type_obj, company=company_obj, **validated_data)
        post_data.save()

        return post_data


class SkillSetSerializer(serializers.ModelSerializer):
    # JobPost는 ManyToMany 관계에 있기 때문에 many=True 사용
    job_posts = JobPostSerializer(many=True)

    class Meta:
        model = SkillSetModel
        fields = ["name", "job_posts"]


class JobPostSkillSetSerializer(serializers.ModelSerializer):
    skill_set = SkillSetSerializer()
    job_post = JobPostSerializer()

    class Meta:
        model = JobPostSkillSetModel
        fields = ["skill_set", "job_post"]


class CompanyBusinessAreaSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    business_area = BusinessAreaSerializer()

    class Meta:
        model = CompanyBusinessAreaModel
        fields = ["company", "business_area"]
