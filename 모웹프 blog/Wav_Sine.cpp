#include <iostream>
#include <math.h>
#include "WavHeader.h"
#define DURATION 10 //(second)
#define SAMPLE_RATE 44100 //(Hz)
#define SINE_FREQUENCY 100 //(Hz)
#define AMPLITUDE 30000 //range of short, –32,768~32,767
#define CHANNEL 1
#define BIT_RATE 16 //16bit-1ch
#define PI 3.141592
int main(void)
{
FILE * f_sine;
f_sine = fopen("./sine.wav", "wb");
int datasize = DURATION * SAMPLE_RATE * CHANNEL * BIT_RATE / 8;
WAV_HEADER header;
memcpy(header.Riff, "RIFF", sizeof(header.Riff));
header.FileSize = datasize + sizeof(WAV_HEADER);
memcpy(header.FileType, "WAVE", sizeof(header.FileType));
memcpy(header.ChunkMarker, "fmt ", sizeof(header.ChunkMarker));
header.FormatLength = 0x10;
header.PCMFormat = WAVE_FORMAT_PCM;
header.Channels = CHANNEL;
header.SampleRate = SAMPLE_RATE;
header.AvgByteRate = SAMPLE_RATE * CHANNEL * BIT_RATE / 8;
header.BlockAlign = CHANNEL * BIT_RATE / 8;
header.BitPerSample = BIT_RATE;
memcpy(header.ChunkDATA, "data", sizeof(header.ChunkDATA));
header.DataSize = datasize;
fwrite(&header, sizeof(WAV_HEADER), 1, f_sine);
short* wav_sine = new short[datasize];
memset(wav_sine,0,sizeof(short)*datasize);
short* itor = wav_sine;
for( int i = 0; i < datasize; i++ )
{
*itor++ = (short)AMPLITUDE*sin(2 * PI * i * SINE_FREQUENCY
/ SAMPLE_RATE);
}
fwrite(wav_sine, 1, datasize, f_sine);
fclose(f_sine);
delete[] wav_sine;
return 0;
}