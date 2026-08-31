def check_type(variable, variableName, dtype, child=None):
    if type(variable) is not dtype:
        raise TypeError(f"Expected {variableName} to be {dtype.__name__} but got {type(variable).__name__}")
    if child is not None:
        for elm in variable:
            if type(elm) is not child:
                raise TypeError(f"Expected {variableName} to be a list of {child.__name__} but found {elm!r} ({type(elm).__name__})")
