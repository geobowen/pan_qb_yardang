# coding=utf-8
import cdsapi
 
c = cdsapi.Client()
for year in range(1981,1991 ):
    for month in range(1, 13):
        outpath = 'D:\\Project\\pan_qaidam_yardang\\wind\\1981-1990\\u\\' + 'u_' + str(year) + str(month).zfill(2) + '.nc'
        print(outpath)
        c.retrieve(
            'reanalysis-era5-land',
            {
                'variable': [
                '10m_u_component_of_wind', 
                ],
                'year': str(year),
                'month': [
                    str(month).zfill(2)
                ],
                'day': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                    '13', '14', '15',
                    '16', '17', '18',
                    '19', '20', '21',
                    '22', '23', '24',
                    '25', '26', '27',
                    '28', '29', '30',
                    '31',
                ],
                'time': [
                    '00:00', '01:00', '02:00',
                    '03:00', '04:00', '05:00',
                    '06:00', '07:00', '08:00',
                    '09:00', '10:00', '11:00',
                    '12:00', '13:00', '14:00',
                    '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00',
                    '21:00', '22:00', '23:00',
                ],
                'area': [
                    39, 90, 36,
                    97,
                ],
                'grid': [0.1, 0.1
                ],
            'format': 'netcdf',
            },
            outpath)