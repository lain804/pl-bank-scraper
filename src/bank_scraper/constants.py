from decimal import Decimal

EXIT_FAILURE = 1
EXIT_SUCCESS = 0

KiB = 1024
MiB = 1024 * KiB
GiB = 1024 * MiB
TiB = 1024 * GiB

KB = 1000
MB = 1000 * KB
GB = 1000 * MB
TB = 1000 * GB

ms = Decimal(0.001)

__all__ = [
    "EXIT_FAILURE",
    "EXIT_SUCCESS",
    "KiB",
    "MiB",
    "GiB",
    "TiB",
    "KB",
    "MB",
    "GB",
    "TB",
    "ms"
]