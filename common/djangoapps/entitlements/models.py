from django.db import models
from django.contrib.auth.models import User
from course_modes.models import CourseMode
from opaque_keys.edx.keys import CourseKey


class CourseEntitlement(models.Model):
    """
    Represents a Student's Entitlement to a Course Run for a given Course.
    """

    user_id = models.ForeignKey(User)
    # TODO: Lookup the Course ID Implementation in
    # the enrollment Model and elsewhere and immitate
    # TODO: Consider replacing with an integer Foreign key and a Course Table
    root_course_id = models.CharField(max_length=250)

    enroll_end_date = models.DateTimeField(null=False)

    mode = models.CharField(default=CourseMode.DEFAULT_MODE_SLUG, max_length=100)

    enrollment_course_id = models.ForeignKey('student.CourseEnrollment', null=True)

    is_active = models.BooleanField(default=1)

    @classmethod
    def entitlements_for_username(cls, username):
        # TODO: Update to use the user provided
        user = User.objects.get(username=username)
        return cls.objects.filter(user_id=user)

    @classmethod
    def entitlements_for_user(cls, user):
        return cls.objects.filter(user_id=user)

    @classmethod
    def get_user_course_entitlement(cls, user, course):
        # TODO: Implement check to see if the Course ID is valid
        return cls.objects.filter(user_id=user, root_course_id=course).first()

    @classmethod
    def set_entitlement_enrollment(cls, user, course_key, course_enrollment):
        course = course_key.org + '+' + course_key.course
        return cls.objects.filter(
            user_id=user,
            root_course_id=course
        ).update(enrollment_course_id=course_enrollment)

    @classmethod
    def remove_enrollment(cls, user, course_key):
        course = course_key.org + '+' + course_key.course
        return cls.objects.filter(
            user_id=user,
            root_course_id=course
        ).update(enrollment_course_id=None)
