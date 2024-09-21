<script>
  import * as d3 from "d3";
  import colors from '../data/colors.json';

  export let color, data, width;

  $: xScale = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, width])
  
  const barColor = color.indexOf('-') > 0 ? color.slice(0, color.indexOf('-')) : color;
</script>

{#each data as d}
	<div class="bar" 
      style="width: { xScale(d) }px; background-color: { barColor };">
		<p>{d}</p>
	</div>
{/each}

<style>
.bar {
  padding: 3px;
  margin: 1px;
  text-align: right;
  color: white;
}
</style>
