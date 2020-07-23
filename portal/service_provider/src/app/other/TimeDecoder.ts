import * as moment from 'moment';

export class TimeDecoder {

  public timeConvert(time: any): String {
    return (time / 24 / 60).toFixed(0) + ':'
      + (time / 60 % 24).toFixed(0) + ':' + (time % 60).toFixed(0);
  }

  public static secondsToDate(time: number): any {
    const year = moment.unix(time).format('YYYY');
    const month = parseFloat(moment.unix(time).format('MM'));
    const date = moment.unix(time).format('DD');
    const mDate = moment([year, month - 1, date]);
    return mDate;
  }

  public static secondsToHMS(d: number): string {
    const h = Math.floor(d / 3600);
    const m = Math.floor(d % 3600 / 60);
    const s = Math.floor(d % 3600 % 60);

    const hDisplay = h > 0 ? h + (h === 1 ? ' hour, ' : ' hours, ') : '';
    const mDisplay = m > 0 ? m + (m === 1 ? ' minute, ' : ' minutes, ') : '';
    const sDisplay = s > 0 ? s + (s === 1 ? ' second' : ' seconds') : '';
    return hDisplay + mDisplay + sDisplay;
  }

  public static secondsToHmsIn12Hour(d: number): string {
    const h = Math.floor(d / 3600);
    const m = Math.floor(d % 3600 / 60);
    const s = Math.floor(d % 3600 % 60);

    let hDisplay = h > 0 ? h + (h === 1 ? '' : '') : '';
    let mDisplay = m > 0 ? m + (m === 1 ? '' : '') : '';
    // var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";
    if (hDisplay.toString().length === 1) {
      if (parseFloat(hDisplay) === 0) {
        hDisplay = '00';
      } else {
        hDisplay = '0' + hDisplay;
      }
    } else if (hDisplay === '') {
      hDisplay = '00';
    }

    if (mDisplay.toString().length === 1) {
      if (parseFloat(mDisplay) === 0) {
        mDisplay = '00';
      } else {
        mDisplay = '0' + mDisplay;
      }
    } else if (mDisplay === '') {
      mDisplay = '00';
    }
    return this.convert24To12Hour(hDisplay + ':' + mDisplay);
  }

  public static secondsToHmsIn24Hour(d: number): string {
    const h = Math.floor(d / 3600);
    const m = Math.floor(d % 3600 / 60);
    const s = Math.floor(d % 3600 % 60);

    let hDisplay = h > 0 ? h + (h === 1 ? '' : '') : '';
    let mDisplay = m > 0 ? m + (m === 1 ? '' : '') : '';
    // var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";
    if ((hDisplay.toString().length < 2) && (parseFloat(hDisplay) < 0)) {
      hDisplay = '0' + hDisplay;
    } else if (!(parseFloat(hDisplay) < 0)) {
      hDisplay = '00';
    }
    if ((mDisplay.toString().length < 2) && (parseFloat(mDisplay) < 1)) {
      mDisplay = '0' + mDisplay;
    } else if (!(parseFloat(mDisplay) < 0)) {
      mDisplay = '00';
    }
    return hDisplay + ':' + mDisplay;
  }

  public static convert24To12Hour(time: any): string {
    time = time
      .toString()
      .match(/^([01]\d|2[0-3])(:)([0-5]\d)(:[0-5]\d)?$/) || [time];
    if (time.length > 1) {
      time = time.slice(1);
      time[5] = +time[0] < 12 ? ' am' : ' pm';
      time[0] = +time[0] % 12 || 12;
    }
    return time.join('');
  }

  public static convert24TextToSeconds(tText: string, seperator: string): Number {
    let seconds = 0;
    try {
      const hh_mm = tText.split(seperator);
      const hh = parseFloat(hh_mm[0]);
      const mm = parseFloat(hh_mm[1]);
      const ss = parseFloat(hh_mm[2]);
      if (hh < 24 && hh > 0) {
        seconds = hh * 3600;
      } else {
        return seconds;
      }
      if (mm < 60 && mm > 0) {
        seconds = seconds + (mm * 60);
      } else {
        return seconds;
      }
      if (ss < 60 && ss > 0) {
        seconds = seconds + ss;
      } else {
        return seconds;
      }
    } catch {
      return seconds;
    }
    return seconds;
  }

}
