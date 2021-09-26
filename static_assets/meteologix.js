// from https://stackoverflow.com/a/3067896
Date.prototype.yyyymmdd = function() {
  var mm = this.getUTCMonth() + 1; // getMonth() is zero-based
  var dd = this.getUTCDate();

  return [this.getUTCFullYear(),
          (mm>9 ? '' : '0') + mm,
          (dd>9 ? '' : '0') + dd
         ].join('');
};

const AVAILABLE_RUN_DELAY_HOURS = 4 // hours before the run becomes available
const RUN_HOURS_UTC = [18, 12, 6, 3, 0]

const getMeteologixUrl = (regionCode) => {
  const targetHourUTC = (new Date()).getUTCHours() + 1 // we round up the hour
  const latestRunHourUTC = RUN_HOURS_UTC.find(runHour => runHour + AVAILABLE_RUN_DELAY_HOURS <= targetHourUTC)
  console.log(latestRunHourUTC)
  const hoursOffset = targetHourUTC - latestRunHourUTC;

  const paddedLatestRunHourUTC = (latestRunHourUTC > 9 ? '' : '0') + latestRunHourUTC
  const runDateTime = `${(new Date()).yyyymmdd()}${paddedLatestRunHourUTC}`

  return `https://img3.meteologix.com/images/data/cache/model/complete_model-en-339-0_modfrahd_${runDateTime}_${hoursOffset}_${regionCode}_200.png`
}
