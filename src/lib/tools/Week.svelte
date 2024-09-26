<script>
    export let data;

    $: formDates = data.map((d) => new Date(d))

    // TODO: style the cards better
    // TODO: add day of the week to cards as well
    // also add which year it is somewhere!
</script>

<div>
    <div class="row">
        {#each data as d}
            <div class="card">
                <p>
                    { d }
                </p> 
            </div>
        {/each}
    </div>
</div>

<style scoped>
.card {
    text-align: center;
    width: fit-content;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    border-radius: 15px;
}

.card:hover {
    cursor: pointer;
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}

.row {
    width: 100%;
    display: flex;
    flex-flow: row wrap;
}
</style>
