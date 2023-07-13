import logging

"""A Python SDK for interacting with the Fly.io API."""

__version__ = "0.1"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

DEFAULT_API_TIMEOUT = 60

FLY_MACHINE_DEFAULT_CPU_COUNT = 1
FLY_MACHINE_DEFAULT_MEMORY_MB = 256
FLY_MACHINE_DEFAULT_WAIT_TIMEOUT = 60

FLY_MACHINES_API_DEFAULT_API_HOSTNAME = "https://api.machines.dev"
FLY_MACHINES_API_VERSION = 1

FLY_MACHINE_STATES = [
    "created",
    "starting",
    "started",
    "stopping",
    "stopped",
    "replacing",
    "destroying",
    "destroyed",
]

FLY_REGIONS = [
    "ams",  # Amsterdam, Netherlands
    "arn",  # Stockholm, Sweden
    "bog",  # Bogotá, Colombia
    "bos",  # Boston, Massachusetts (US)
    "cdg",  # Paris, France
    "den",  # Denver, Colorado (US)
    "dfw",  # Dallas, Texas (US)
    "ewr",  # Secaucus, NJ (US)
    "fra",  # Frankfurt, Germany
    "gdl",  # Guadalajara, Mexico
    "gig",  # Rio de Janeiro, Brazil
    "gru",  # São Paulo
    "hkg",  # Hong Kong, Hong Kong
    "iad",  # Ashburn, Virginia (US)
    "jnb",  # Johannesburg, South Africa
    "lax",  # Los Angeles, California (US
    "lhr",  # London, United Kingdom
    "maa",  # Chennai (Madras), India
    "mad",  # Madrid, Spain
    "mia",  # Miami, Florida (US)
    "nrt",  # Tokyo, Japan
    "ord",  # Chicago, Illinois (US)
    "otp",  # Bucharest, Romania
    "qro",  # Querétaro, Mexico
    "scl",  # Santiago, Chile
    "sea",  # Seattle, Washington (US)
    "sin",  # Singapore, Singapore
    "sjc",  # San Jose, California (US)
    "syd",  # Sydney, Australia
    "waw",  # Warsaw, Poland
    "yul",  # Montreal, Canada
    "yyz",  # Toronto, Canada
]

FLY_APP_VM_SIZES = [
    "shared-cpu-1x",
    "dedicated-cpu-1x",
    "dedicated-cpu-2x",
    "dedicated-cpu-4x",
    "dedicated-cpu-8x",
]

FLY_MACHINE_VM_SIZES = [
    "shared-cpu-1x",
    "shared-cpu-2x",
    "shared-cpu-4x",
    "shared-cpu-8x",
    "performance-1x",
    "performance-2x",
    "performance-4x",
    "performance-8x",
    "performance-16x",
]
