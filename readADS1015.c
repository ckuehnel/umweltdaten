# Source: http://blog.generationmake.de/articles/14/analog-digital-wandler-ads1015-fuer-den-raspberry-pi

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <linux/i2c-dev.h>
#include <fcntl.h>
#include <unistd.h>

unsigned short int swap_bytes(unsigned short int input)
{
	return (((input & 0xff) << 8) | ((input >> 8) & 0xff));
}

int read_channel(unsigned int channel, int file)
{
	int adc_data=0,x=0;

	if(channel>3) return -1;
	i2c_smbus_write_word_data(file,0x01,swap_bytes((0xc383|(channel<<12))));
	do
	{
		x=swap_bytes(i2c_smbus_read_word_data(file, 0x01));	// config register
		printf("Config register: 0x%04x\n", x);
	} while(!(x&0x8000));
	adc_data=swap_bytes(i2c_smbus_read_word_data(file, 0x00));	// conversion register
	printf("Conversion register (channel %i): 0x%04x = %i\n\n", channel, adc_data,adc_data);
	return adc_data;
}

int main(void)
{
	int file;

	printf("Texas Instruments ADS1015\n\n");
	if((file=open("/dev/i2c-1",O_RDWR))<0)	// open i2c-bus
	{
		perror("cannot open i2c-1");
		exit(1);
	}
	if(ioctl(file, I2C_SLAVE, 0x48)<0)	// open slave, address ADS1015 = 0x48 with ADDR grounded
	{
		perror("cannot open slave address");
		exit(1);
	}

	read_channel(0,file);
	read_channel(1,file);
	read_channel(2,file);
	read_channel(3,file);

	close(file);

	return 0;
}