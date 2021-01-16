# Evan Widloski - 2020-08-01
# Logging/Plotting utility for Jim

import sys
import redpitaya_scpi as scpi
import matplotlib.pyplot as plt
from datetime import datetime
import time
import numpy as np
import argparse
from os.path import basename

csv_format = ""

def acquire(host, decimation):
    """Acquire data from redpitaya input channels

    Args:
        args.host (str): redpitaya host address
        args.decimation (int): sample decimation

    Returns:
        complex ndarray of samples
    """

    rp_s = scpi.scpi(host)

    sample_rate = 125e6 / decimation

    rp_s.tx_txt('ACQ:DEC {}'.format(decimation))
    rp_s.tx_txt('ACQ:START')
    # https://redpitaya.readthedocs.io/en/latest/appsFeatures/examples/acqRF-samp-and-dec.html#s-rate-and-dec
    # allow time for finishing acquisition, plus a little extra
    time.sleep(131.072e-6 * decimation + 1)
    rp_s.tx_txt('ACQ:TRIG:DLY 0')
    rp_s.tx_txt('ACQ:TRIG NOW')

    while 1:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            break

    def buff_to_float(buff_string):
        """Convert buffer string to list of floats"""
        buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
        return list(map(float, buff_string))

    rp_s.tx_txt('ACQ:SOUR1:DATA?')
    v1 = np.array(buff_to_float(rp_s.rx_txt()))
    rp_s.tx_txt('ACQ:SOUR2:DATA?')
    v2 = np.array(buff_to_float(rp_s.rx_txt()))

    return v1 + 1j * v2


def plot(args):
    """Plot samples from redpitaya

    Args:
        args.filename (str): csv of logged data to plot.  if None, samples are acquired
    """

    if args.filename is None:
        x = acquire(args.host, args.decimation)
    else:
        # FIXME, load decimation
        x = np.loadtxt(args.filename).view(complex)


    num_samples = len(x)
    sample_rate = 125e6 / args.decimation

    plt.figure(figsize=(10, 7))

    plt.subplot(3, 1, 1)
    v1 = x.real
    v2 = x.imag
    t = np.linspace(0, num_samples / sample_rate, num_samples)
    plt.plot(v1)
    plt.plot(v2)
    plt.legend(['V1', 'V2'])
    plt.ylabel('Voltage')
    plt.xlabel('Sample #')

    f, mag, phase = mag_phase(x, sample_rate)

    plt.subplot(3, 1, 2)
    plt.plot(f, mag)
    plt.xlabel('Frequency')
    plt.ylabel('Power (dBm)')

    plt.subplot(3, 1, 3)
    plt.plot(f, phase)
    plt.xlabel('Frequency')
    plt.ylabel('Phase (radians)')

    plt.tight_layout()
    plt.show()


def mag_phase(x, sample_rate):
    """Compute magnitude of input signal in dBm and phase in radians"""

    num_samples = len(x)
    f = np.linspace(-sample_rate / 2, sample_rate / 2, num_samples)
    X = np.fft.fftshift(np.fft.fft(x)) / num_samples
    mag = 10 * np.log10((np.abs(X)**2 / 50) / 1e-3)
    phase = np.angle(X)

    return f, mag, phase


def log(args):
    """Log redpitaya data to file"""

    x = acquire(args.host, args.decimation)

    sample_rate = 125e6 / args.decimation

    if args.filename:
        filename = args.filename
    else:
        filename = datetime.now().isoformat() + '.csv'

    # FIXME, save decimation
    np.savetxt(
        filename,
        x.view(float),
        delimiter=',',
        # header='sample_rate={}\nreal,imaginary'.format(sample_rate)
        header='sample_rate={}'.format(sample_rate)
    )

# def spec(args):
#     """Convert IQ samples to spectrogram and save to file"""

#     sample_rate = 125e6 / args.decimation

#     x = np.loadtxt(args.input).view(complex)
#     f, mag, _ = mag_phase(x, sample_rate)

#     if args.output is None:
#         args.output = basename(args.input).rstrip('.csv') + '_spec.csv'

#     np.savetxt(args.output, np.vstack((f, mag)).T)


def fft(args):
    """Convert IQ samples to mag/phase and save to file"""

    sample_rate = 125e6 / args.decimation

    x = np.loadtxt(args.input).view(complex)

    f, mag, phase = mag_phase(x, sample_rate)

    if args.output is None:
        args.output = basename(args.input).rstrip('.csv') + '_fft.csv'

    np.savetxt(
        args.output,
        np.vstack((f, mag, phase)).T,
        delimiter=',',
        header='sample_rate={}\nfrequency (rad/s),power (dbm),angle (rad)'.format(sample_rate)
    )


def main():

    parser = argparse.ArgumentParser(description="RedPitaya sampler")

    parser.add_argument('--host', type=str, default='rp-f078bf.local', help="redpitaya host address")
    parser.add_argument('--decimation', type=int, default=8, help="redpitaya sample decimation")

    subparsers = parser.add_subparsers()
    subparsers.required = True

    log_parser = subparsers.add_parser('log', help="log redpitaya data to csv")
    log_parser.add_argument('filename', nargs='?', type=str, default=None, help="path to csv")
    log_parser.set_defaults(func=log)

    plot_parser = subparsers.add_parser('plot', help="plot logged redpitaya waveform")
    plot_parser.add_argument('filename', nargs='?', type=str, help="path to csv")
    plot_parser.set_defaults(func=plot)

    fft_parser = subparsers.add_parser('fft', help="convert raw IQ data to magnitude and phase. outputs to XXX_fft.csv")
    fft_parser.add_argument('input', nargs='?', type=str, help="path to input csv")
    fft_parser.add_argument('output', nargs='?', default=None, type=str, help="path to output csv")
    fft_parser.set_defaults(func=fft)

    args = parser.parse_args()

    args.func(args)


if __name__ == '__main__':
    main()
