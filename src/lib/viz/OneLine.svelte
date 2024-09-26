<script>
    import * as d3 from "d3";

    export let color, width, height, endStops, totalTime;

    const radius = 15;
    const rect = {
        w: width,
        h: 10
    }

    $: xScale = d3.scaleLinear()
    .domain([0, d3.max(totalTime)])
    .range([0, width]);

    function getDuration(seconds) {
        const mins = Math.floor(seconds / 60);
        const hours = Math.floor(mins / 60);
        const minsPlural = mins > 1 ? 's' : '';
        const hoursPlural = hours > 1 ? 's' : '';
        return mins > 60 ? `${ hours } hour${ hoursPlural }, ${ mins % 60 } minute${ minsPlural }, ${ seconds % 60 } seconds` :
        seconds > 60 ? `${ mins } minute${ minsPlural }, ${ seconds % 60 } seconds` : `${ seconds } secs`
    }
</script>


<svg {width} {height} viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin">
        <g>
            {#each totalTime as t}
            <rect
                x={ radius }
                y={ height/2 + radius/2 + 3 }
                width={ xScale(t) }
                height={ rect.h }
                stroke={ color } 
                fill={ color }
                fill-opacity={ 0.5 } />
            {/each}

            {#each endStops as d, i}
                <text
                    fill='black'
                    text-anchor={ i > 0 ? 'end' : 'start'}
                    x={ i > 0 ? width : radius }
                    y={ height - 10 }
                    dx={ -4 }
                    dy="0.35em">
                        { d.stop_name }
                    </text>

                <circle 
                    cx={ i > 0 ? rect.w - radius : radius } 
                    cy={ height/2 + radius } 
                    r={ radius } 
                    fill={ color } />
                
                <circle 
                    cx={ i > 0 ? rect.w - radius : radius } 
                    cy={ height/2 + radius } 
                    r={ radius/2 } 
                    fill="white" />
            {/each}

            <text
                fill='black'
                text-anchor="middle"
                x={ width/2 }
                y={ 10 }
                dx={ -4 }
                dy="0.35em">
                The average duration of this trip was { getDuration(totalTime[1]) + ' long' }
            </text>

            <text
                fill='black'
                text-anchor="middle"
                x={ width/2 }
                y={ height - 10 }
                dx={ -4 }
                dy="0.35em">
                While the total average wait time for stops was { getDuration(totalTime[0]) }
            </text>
        </g>
</svg>
