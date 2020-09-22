from obspy import read
st = read("/home/incyt/servicio/uploads/GI_ISE2I_02_BDF_D_2020-09-09T06:49:57.327.mseed")
st += read("/home/incyt/servicio/uploads/GI_ISE2I_02_BDF_D_2020-09-09T07:00:00.001.mseed")
st += read("/home/incyt/servicio/uploads/GI_ISE2I_02_BDF_D_2020-09-09T08:59:32.959.mseed")
#st += read("/home/incyt/servicio/uploads/.mseed")

#st += read("/home/incyt/servicio/uploads/GI_ISE2I_0_BDF_D_2020-08-25T18:49:57.034.mseed")

st.filter('bandpass', freqmin=0.1, freqmax=25, corners=2, zerophase=True)

print(st)
st.plot(type='dayplot')
st.plot()
