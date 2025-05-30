class BaseLogger:
    def list_attr(self, sep: str = ', ') -> str:
        """
        	Return a string representation of all attributes of the instance,
        	formatted as 'key=value' pairs joined by the specified separator.
        """
        attrs = [f"{k} = {v!r}" for k, v in self.__dict__.items()]

        return sep.join(attrs)
    
    def list_attr_exc(self, *excludes: str, sep: str = ', ') -> str:
        """
        	Return a string representation of instance attributes excluding the specified ones.
        """
        attrs = [
            f"{k} = {v!r}"
            for k, v in self.__dict__.items()
            if k not in excludes
        ]
        
        return sep.join(attrs)
    
    def list_attr_inc(self, *includes: str, sep: str = ', ') -> str:
        """
			Return a string representation of only the specified instance attributes.
        """
        attrs = [
            f"{k} = {self.__dict__[k]!r}"
            for k in includes
            if k in self.__dict__
        ]
        
        return sep.join(attrs)