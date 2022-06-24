from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import (
    JobPostSkillSet,
    JobType,
    JobPost,
    Company
)

from .serializers import (
    CompanySerializer,
    JobTypeSerializer,
    JobPostSerializer,
)

from django.db.models.query_utils import Q


class SkillView(APIView):
    permission_classes = [permissions.AllowAny]

    # JobPostSerializer 사용
    # 고정적으로 두개의 기술 스택(예 : django, mysql)을 요구하는 회사 검색
    # Q, field lookup 사용

    def get(self, request):
        # query_params ?
        # getlist ?

        # https://www.django-rest-framework.org/api-guide/requests/
        # request.query_params 동의어? request.GET

        # request.GET.get("skills", "")와 비슷한 것 같음 (?)
        skills = self.request.query_params.getlist('skills', '')
        # print("skills = ", end=""), print(skills)

        # python과 mysql만 조건으로 넣어줄 경우
        # job_skills = JobPostSkillSet.objects.filter(
        #     Q(skill_set__name="python") | Q(skill_set__name="mysql")
        # )

        query = Q()
        for skill in skills:
            # 역참조, 입력받은 skills만큼 조건 추가
            # 추가 될 경우 OR(|)로 추가
            query.add(Q(skill_set__name=skill), Q.OR)

        # 해당 조건(query)에 부합하는 object 찾기
        job_skills = JobPostSkillSet.objects.filter(query)
        job_posts = JobPost.objects.filter(
            # in : 튜플, 리스트 스트링 / 쿼리셋과 같은 객체를 대상으로 조회
            # 여기서는 id를 기준으로 리스트 검색
            id__in=[job_skill.job_post.id for job_skill in job_skills])

        # job_posts에 해당 레코드가 존재하면?
        if job_posts.exists():
            # 다수의 jobpost가 있을 수 있기 때문에 many=True 지정
            job_serializer = JobPostSerializer(job_posts, many=True)
            return Response(job_serializer.data, status=status.HTTP_200_OK)

        return Response({"fail": "조회 실패"}, status=status.HTTP_400_BAD_REQUEST)


class JobView(APIView):
    # job_type이 테이블에 존재하지 않는 데이터면 HTTP 400 Error 반환
    # 회사 이름이 존재하지 않으면 생성해서 등록

    # 조건 : request1 : job_type을 id값으로
    # 조건 : request2 : job_type을 type명으로

    def post(self, request):
        job_type = int(request.data.get("job_type", None)) # Integer로 받기(id)
        # job_type = request.data.get("job_type", None) # String으로 받기(type 이름)
        company_name = request.data.get("company_name", None)
        # job_description = request.data.get("job_description", None)
        # salary = int(request.data.get("salary", None))

        # 입력받은 데이터 값 저장
        # data = request.data

        # 모델에서 해당 object를 찾아준다.
        job_type_obj = JobType.objects.get(id=job_type) # Integer로 찾기(id)
        # job_type_obj = JobType.objects.get(job_type=job_type) # String으로 찾기(type 이름)
        company_name_obj = Company.objects.get(company_name=company_name)

        # JobPost 모델에 있는 필드에 찾은 object를 넣어주는데
        # 해당 object를 넣으면 오류가 발생하기 때문에
        # serializer를 사용하여 json 데이터로 넣어준다.
        request.data["job_type"] = JobTypeSerializer(job_type_obj).data
        request.data["company"] = CompanySerializer(company_name_obj).data

        # JobPostSerializer에 받은 데이터를 넣어줌
        job_serializer = JobPostSerializer(data=request.data)

        if job_serializer.is_valid():
            job_serializer.save()
            return Response({"success": "등록 완료"}, status=status.HTTP_200_OK)

        return Response({"success": "등록 실패"}, status=status.HTTP_400_BAD_REQUEST)


    # ↓ 아침 퀴즈 해설 ↓

    # def post(self, request):
    #     job_type = int(request.data.get("job_type", None))
    #     company_name = request.data.get("company_name", None)

    #     job_type_obj = JobType.objects.filter(id=job_type)
    #     # 만약 request.data로 받은 job_type이 없다면?
    #     if not job_type_obj.exists():
    #         return Response({"fail": "존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

    #     company_obj = Company.objects.filter(company_name=company_name)
    #     # 만약 request.data로 받은 company_name이 없다면?
    #     if not company_obj.exists():
    #         # 새롭게 추가
    #         company = Company(company_name=company_name).save()
    #     else:
    #         # 기존 값을 찾아 그대로 저장
    #         company = company_obj.first()

    #     job_serializer = JobPostSerializer(data=request.data)
    #     if job_serializer.is_valid():
    #         job_serializer.save(job_type=job_type_obj, company=company)
    #         return Response({"success": "등록 완료"}, status=status.HTTP_200_OK)

    #     return Response({"success": "등록 실패"}, status=status.HTTP_400_BAD_REQUEST)
