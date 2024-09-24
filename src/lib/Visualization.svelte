<script>
  import Barplot from './viz/Barplot.svelte';
  import TrainLine from './viz/TrainLine.svelte';
  import allTrips from './data/grouped_trips.json';
  import Labels from './viz/Labels.svelte';
  import OneLine from './viz/OneLine.svelte';

  const select = allTrips.trips[0]
  const line = select.route_id;
  const stops = select.stops.map((t) => t.stop_name);
  const waitData = select.stops.map((t) => t.avg_wait_time);

  const currColor = line.indexOf('-') > 0 ? line.slice(0, line.indexOf('-')) : line;
</script>

<div class="visualization">
  <div>
    <OneLine color={currColor} width={800} height={50} />
  </div>
  <div>
    <Labels data={stops} width={200} height={400} />
    <TrainLine color={currColor} data={waitData} width={40} height={400} />
    <Barplot color={currColor} data={waitData} width={400} height={400} />
  </div>
</div>