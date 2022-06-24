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
    JobPostSerializer,
    JobPostSkillSetSerializer
)

from django.db.models.query_utils import Q


class SkillView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        skills = self.request.query_params.getlist('skills', '')
        print("skills = ", end=""), print(skills)

        return Response(status=status.HTTP_200_OK)


class JobView(APIView):
    def post(self, request):
        # job_type = int(request.data.get("job_type", None))
        # company_name = request.data.get("company_name", None)
        # job_description = request.data.get("job_description", None)
        # salary = int(request.data.get("salary", None))

        data = request.data
        job = JobPost.objects.create(**data)
        job.save()

        # job_serializer = JobPostSkillSetSerializer(data=request.data)

        # if job_serializer.is_valid:
        #     job_serializer.save()

        #     return Response({"success": "등록 완료"}, status=status.HTTP_200_OK)

        return Response({"success": "등록 완료"}, status=status.HTTP_200_OK)
