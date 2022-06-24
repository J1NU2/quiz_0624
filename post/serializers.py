from rest_framework import serializers

from post.models import Company as CompanyModel
from post.models import JobPost as JobPostModel
from post.models import JobPostSkillSet as JobPostSkillSetModel

# 1. Company Serializer (model = Company) 구현**
# 2. JobPost Serializer (model = JobPost) 구현**
# 3. JobPostSkillSet Serializer (model = JobPostSkillSet) 구현**

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = ["id", "company_name"]


class JobPostSkillSetSerializer (serializers.ModelSerializer):
    class Meta:
        model = JobPostSkillSetModel
        fields = ["skill_set", "job_post"]


class JobPostSerializer(serializers.ModelSerializer):
    position_type = serializers.SerializerMethodField()
    company = CompanySerializer()
    skiilsets = JobPostSkillSetSerializer(many=True)

    def get_position_type(self, obj):
        type_name = obj.position_type.job_type
        return type_name

    class Meta:
        model = JobPostModel
        fields = ["position_type", "company", "job_description", "salary", "skiilsets"]
