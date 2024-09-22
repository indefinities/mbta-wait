<script>
  import Barplot from './viz/Barplot.svelte';
  import TrainLine from './viz/TrainLine.svelte';
  import allTrips from './data/filtered_trips.json';
  import Labels from './viz/Labels.svelte';

  const select = allTrips.trips[0]
  const line = select.route_id;
  const schedule = select.schedule;
  const stops = schedule.map((t) => t.stop_name);
  const waitData = schedule.map((t) => t.wait_time);

  const currColor = line.indexOf('-') > 0 ? line.slice(0, line.indexOf('-')) : line;
</script>

<div class="visualization">
  <Labels data={stops} width={200} height={400} />
  <TrainLine color={currColor} data={waitData} width={40} height={400} />
  <Barplot color={currColor} data={waitData} width={400} height={400} />
</div>