type APIParams = {
    headers: {
        Authorization: string
    }
}

const apiUrl: string = 'https://api-v3.mbta.com/';
const apiKey: string = '68445b21a9af4adebbd6dd1b094029b2';
const params: APIParams = {
    headers: {
        'Authorization': `Bearer ${apiKey}`,
    },
}

async function getRouteData(): Promise<string|undefined> {
    const queryParams: string = 'routes?filter[type]=0,1';
    try {
        const response = await fetch(`${apiUrl}${queryParams}`, params);
        if (response.ok) {
            const data = await response.json()
            return data;
        }
    } catch (error) {
        console.log(error)
        throw new Error()
    }
}

export { getRouteData }
