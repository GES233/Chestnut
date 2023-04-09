

async function fetchPosts(url: string): Promise<any> {
    let response = await fetch(url);
    let body = await response.json();
    return body;
}