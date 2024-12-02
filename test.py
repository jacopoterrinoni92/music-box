import spidev

spi = spidev.SpiDev()

spi.open(0,0)

# Configure the SPI bus
spi.max_speed_hz = 1000000  # Set the maximum SPI clock speed
spi.mode = 0  # Set the SPI mode (0 or 1)

# Send a byte and receive a byte
response = spi.xfer2([0x01])

# Close the SPI device
spi.close()