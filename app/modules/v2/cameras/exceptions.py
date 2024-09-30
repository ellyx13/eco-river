from exceptions import CustomException
from core.exceptions import ErrorCode as CoreErrorCode



class ErrorCode(CoreErrorCode):
    @staticmethod
    def DontSupportConningCameraWithoutLink():
        return CustomException (
            type="cameras/info/dont-support-conning-camera-without-link",
            status=400,
            title="Don't support conning camera without link.",
            detail="The camera link must be provided."
        )