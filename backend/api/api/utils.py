class Utils:
    
    def error_msg(code: str, msg: str):
        """Generate error msg to include in detail of exceptions

        Args:
            code (str): error code
            msg (str): error menssage

        Returns:
            Dict: dictionary with the error details
        """
        return {
            "error": {
                "msg": msg,
                "code": code
            }
        }