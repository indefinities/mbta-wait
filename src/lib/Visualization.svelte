<script>
// Svelte component imports
  import Barplot from './viz/Barplot.svelte';
  import TrainLine from './viz/TrainLine.svelte';
  import OneLine from './viz/OneLine.svelte';
  import Week from './tools/Week.svelte';

// data imports
  import allTrips from './data/grouped_trips.json';
  import currDates from './data/curr_dates.json';

  export let width, height

  const dates = currDates.dates;

  const select = allTrips.trips[4]
  const line = select.route_id;
  const allStops = select.stops;
  const color = line.indexOf('-') > 0 ? line.slice(0, line.indexOf('-')) : line;

  const totalWaitTime = allStops.reduce((sum, stop) => sum + stop.avg_wait_time, 0);
  const totalTripTime = select.total_trip_time;
  const totalTime = [totalWaitTime, totalTripTime]
  const dataCopy = allStops.slice();
  const endStops = [ dataCopy.shift(), dataCopy.pop() ];
</script>

<div class=" viz centered-page">
  <div class="centered-section">
    <Week data={dates} />
  </div>
  <div class="centered-section">
    <h3>The Average Wait Time for Each Stop</h3>
    <TrainLine {color} {height} width={width/3} data={allStops} />
    <Barplot {color} {height} data={allStops} width={2*width/3} />
  </div>

  <div class="centered-section">
    <OneLine {color} width={800} height={80} {endStops} {totalTime} />
  </div>
</div>

<style scoped>
h3 {
  text-align: center;
}
</style>