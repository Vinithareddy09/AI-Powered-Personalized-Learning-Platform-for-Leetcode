import sys


class customexception(Exception):

    def _init_(self,error_message,error_details:sys):
        self.error_message=error_message
        ,,exc_tb=error_details.exc_info()
        print(exc_tb)

        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename

    def _str_(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.error_message))


if _name=="main_":
    try:
        a=1/0

    except Exception as e:
        #print(e)
        raise customexception(e,sys)
