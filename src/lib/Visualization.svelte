<script>
  import Barplot from './viz/Barplot.svelte';
  import allTrips from './data/filtered_trips.json';

  const select = allTrips.trips[3]
  const line = select.route_id;
  const waitData = select.schedule.map((t) => t.wait_time);
</script>

<div class="visualization">
  <Barplot color={line} data={waitData} width={500}/>
</div>