from dataclasses import dataclass


@dataclass
class DataArguments:
    """
    This class is used to store all the data arguments
    """
    ip: str
    protocol: str
    timeout: float
    verbose: bool
    port: int
    number: int
