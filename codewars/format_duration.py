def format_duration(seconds):
    if seconds == 1:
        s1 = '1 second'

    if seconds == 60:
        m1 = '1 minute'

    if seconds == 3600:
        h1 = '1 hour'

    if seconds == 86400:
        d1 = '1 day'

    if seconds == 31536000:
        y1 = '1 year'
        return y1
    if 1 < seconds < 60:
        return seconds+' '+seconds
    elif 60 < seconds < 3600:
        minutes =  seconds/60
        seconds =  seconds%60
        if seconds == 1:
            return minutes + 'minutes and ' + seconds + ' second'
        else:
            return minutes + 'minutes and '+seconds+' seconds'
    elif seconds < 86400 and seconds > 3600:
        hours = seconds/3600
        minutes = (seconds - hours*3600)/60
        seconds = (seconds - hours*3600)- minutes*60
        return hours + ' hours '+minutes+'minutes and '+seconds+' seconds'
    elif seconds< 31536000 and seconds >=86400:
        days = seconds/86400
        left = seconds - days*86400
        if left == 1:
            return days + ' days and 1 seconds '
        hours = left / 3600
        left = left - hours * 3600
        minutes = left / 60
        seconds = left - minutes * 60
        return days + ' days' + hours + ' hours ' + minutes + 'minutes and ' + seconds + ' seconds'
    else:
        years = seconds/31536000
        left = seconds - years*31536000
        days = left / 86400
        left = left - days * 86400
        hours = left / 3600
        left =  left - hours * 3600
        minutes = left / 60
        seconds = left - minutes * 60
        return years+' years'+ days + ' days' +hours + ' hours ' + minutes + 'minutes and ' + seconds + ' seconds'



def integr(seconds):
        if seconds == 1:
            s1 = '1 second'
            return s1
        if seconds ==60:
            m1 = '1 minute'
            return m1
        if seconds == 3600:
            h1 = '1 hour'
            return h1
        if seconds == 86400:
            d1 = '1 day'
            return d1
        if seconds == 31536000:
            y1 = '1 year'
            return y1





