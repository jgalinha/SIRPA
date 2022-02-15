# -*- coding: utf-8 -*-
"""Utils model file

This module define utils helper class, a class with helper methods

@Author: José Galinha
@Email: j.b.galinha@gmail.com
"""


class Utils:
    def error_msg(code: str, msg: str, /, *, error: str = None):
        """Generate error msg to include in detail of exceptions

        Args:
            code (str): error code
            msg (str): error menssage
            error (str): optional error details

        Returns:
            Dict: dictionary with the error details
        """
        return {"error": {"msg": msg, "code": code, "error_detail": error}}
