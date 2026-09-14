# FPGA QPSK Digital Communication Chain

### Fixed-Point DSP, Polyphase FIR and Hardware Optimization in Verilog

## Introduction

This project implements a QPSK digital communication chain from
floating-point modeling in Python to fixed-point RTL implementation
on FPGA.

The system includes PRBS9 generation, QPSK symbol mapping, pulse
shaping using a Raised Cosine FIR filter, configurable sampling-phase
decimation, symbol decision and BER estimation.

The design was first developed and validated in Python using
floating-point arithmetic. The complete chain was then converted to
fixed-point representation, defining the numerical resolution of
each hardware stage and analyzing quantization error and overflow.

The final architecture was implemented in Verilog and validated
through simulation and FPGA testing using Vivado.


## Fixed-Point Design

The floating-point model was converted to fixed-point arithmetic
before the RTL implementation.

The Raised Cosine filter coefficients were normalized and quantized
using different numbers of fractional bits.

The quantization resolution was selected using a Signal-to-Error
Ratio (SRE) criterion of at least 40 dB.

The resulting filter coefficient representation was:

S(8,7)

8 total bits:
- 1 sign bit
- 7 fractional bits
