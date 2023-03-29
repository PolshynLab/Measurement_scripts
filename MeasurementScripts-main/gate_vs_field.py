# Script sweeps one gate  while two other voltages are applied.
# to interrupt the script after line is finished press ESC.
# (for this the script must be run from terminal)
# Revised by Gregory Polshyn on 3/20/2019

import labrad
import numpy
import time
import msvcrt
import os

# Initialization
control_field = False
zero_field_in_the_end = False

third_lockin = False

cxn = labrad.connect()
DV = cxn.data_vault
cxn_2 = labrad.connect()
cxn_3 = labrad.connect()
DAC = cxn.dac_adc
DAC.select_device()
LA1 = cxn.sr830
LA1.select_device(0)
LA2 = cxn_2.sr830
LA2.select_device(1)
#if third_lockin:
#    LA3 = cxn_3.sr830
#    LA3.select_device()   # change accordingly
#if control_field:
   # MG = cxn.ami_430
   # MG.select_device()

# output
file_path = "GP39"
file_name = "GP39"

number_of_points = 2000
number_of_field_points = 1
tcdel = 0.4

voltage_sweep_range = [-2.5, 2.5]
field_sweep_range = [-1.0, 1.0]

#lockin parameters
amplitude = 0.5
frequency = 17.77
time_constant = 0.1

v_gate2 = 1.0  #other gate
v_bias = 2.0

dc_channel_gate = 1     # gate voltage swept
dc_channel_gate2 = 2    # other gate
dc_channel_bias = 3     # bias current

# gains for dac_adc channels
sensitivity_1 = LA1.sensitivity()
sensitivity_2 = LA2.sensitivity()
print(sensitivity_2)
# = LA2.sensitivity()['V']
if third_lockin:
    sensitivity_3 = LA3.sensitivity()#['V']
print('Sensitivity 1:', sensitivity_1, 'Sensitivity 2:', sensitivity_2)
current_gain = 1e-6
# adc_gains = [current_gain*sensitivity_1/10, sensitivity_2/10, sensitivity_2/10, 1]
adc_gains = [1, 1, 1, 1]

# setting time constants
LA1.time_constant(time_constant)
LA2.time_constant(time_constant)
if third_lockin:
    LA3.time_constant(time_constant)

wait_time = 1e6*tcdel*time_constant


def ramp_field(mg, field_setpoint):
    print('Ramping field to', field_setpoint, 'T...')
    mg.conf_field_targ(field_setpoint)
    mg.ramp()
    target_field = float(mg.get_field_targ())
    actual_field = float(mg.get_field_mag())
    while abs(target_field - actual_field) > 1e-3:
        time.sleep(4)
        actual_field = float(mg.get_field_mag())
    print('Target field reached.')


def main():
    start = time.time()
    scriptname = os.path.basename(__file__)
    print("Running ", scriptname)
    os.system('title '+scriptname)

    LA1.sine_out_amplitude(amplitude)
    LA1.frequency(frequency)
    time.sleep(4)

    try:
        DV.mkdir(file_path)
        DV.cd(file_path)
    except Exception:
        DV.cd(file_path)
    DV.new(file_name, ("voltage_index", "field_index",  "magnetic_field", "vg"), ('ix', 'iy', 'vx', 'vy'))
    DV.add_parameter('number of points', number_of_points)
    DV.add_parameter('lock-in output', amplitude)
    DV.add_parameter('output frequency [Hz]', frequency)
    DV.add_parameter('time constant [s]', time_constant)
    DV.add_parameter('1st lock-in sensitivity', sensitivity_1)
    DV.add_parameter('2nd lock-in sensitivity', sensitivity_2)
    if third_lockin:
        DV.add_parameter('3nd lock-in sensitivity', sensitivity_3)
    DV.add_parameter('data1_col', 7)  # 1
    DV.add_parameter('data1_label', 'V [V]')
    DV.add_parameter('data2_col', 5)  # 2
    DV.add_parameter('data2_label', '  [ ]')
    DV.add_parameter('x_col', 4)
    DV.add_parameter('y_col', 3)
    DV.add_parameter('extent', tuple([voltage_sweep_range[0], voltage_sweep_range[1], field_sweep_range[0], field_sweep_range[1]]))
    DV.add_parameter('pxsize', tuple([number_of_points, number_of_field_points]))
    DV.add_parameter('magnetic_field_pnts', number_of_field_points)
    DV.add_parameter('magnetic_field_rng', (field_sweep_range[0], field_sweep_range[1]))
    DV.add_parameter('vg_pnts', number_of_points)
    DV.add_parameter('vg_rng', (voltage_sweep_range[0], voltage_sweep_range[1]))

    vg = numpy.linspace(voltage_sweep_range[0], voltage_sweep_range[1], number_of_points)
    field = numpy.linspace(field_sweep_range[0], field_sweep_range[1], number_of_field_points)

    start_v = 0.0
    DAC.ramp1(dc_channel_gate2, 0.0, v_gate2, 1000, 2500)
    time.sleep(1)
    DAC.ramp1(dc_channel_bias, 0.0, v_bias, 1000, 2500)
    time.sleep(1)

    kk = 0
    while kk < number_of_field_points:
        print("Line", kk, "out of ", number_of_field_points)
        # if control_field:
            # ramp_field(MG, field[kk])

        print('\r', 'Ramping gate voltages to initial values...')#,
        end_v = voltage_sweep_range[0]
        DAC.ramp1(dc_channel_gate, start_v, end_v, 1000, 2500)
        DAC.set_voltage(dc_channel_gate, end_v)
        time.sleep(5.0)

        start_v = voltage_sweep_range[0]
        end_v = voltage_sweep_range[1]
        print('\r', 'Measuring:' 'Start_V:', start_v, '; End_V:', end_v)#,
        d_tmp = DAC.buffer_ramp([dc_channel_gate], [1, 2, 3, 4], [start_v], [end_v], number_of_points, wait_time, 1)
        print('\r', 'Sweep is over')#,
        start_v = end_v
        aux_1, aux_2, aux_3, aux_4 = d_tmp
        index_g = numpy.linspace(1, number_of_points, number_of_points)
        index_f = numpy.linspace(kk, kk, number_of_points)
        field_line = field[kk] * numpy.ones(number_of_points)

        res_1 = aux_1*adc_gains[0]
        res_2 = aux_2*adc_gains[1]
        res_3 = aux_3*adc_gains[2]
        res_4 = aux_4*adc_gains[3]
        data = numpy.array([index_g, index_f,  field_line, vg, res_1, res_2, res_3, res_4])
        print('Writing Data...')
        DV.add(data.T)

        kk += 1
        # catching  interruption
        if msvcrt.kbhit():
            if ord(msvcrt.getch()) == 27:
                print ('Interrupting the cycle...')
                break

    print('\r','Measurement done. Ramping gate voltages to zero...')#,
    DAC.ramp1(dc_channel_gate, start_v, 0.0, 1000, 2500)
    time.sleep(1)
    DAC.ramp1(dc_channel_gate2, v_gate2, 0.0, 1000, 2500)
    time.sleep(1)
    DAC.ramp1(dc_channel_bias, v_bias, 0.0, 1000, 2500)
    time.sleep(1)
    # if zero_field_in_the_end and control_field:
        # MG.conf_field_targ(0.0)

    end = time.time()
    print("Total time taken: ", end - start, "seconds")
    # print 2*'\a'

if __name__ == '__main__':
    main()