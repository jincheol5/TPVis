async function request_layout(request_json) {
    try {
        const response = await fetch("http://localhost:5000/compute_layout", {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify(request_json)
        });
        const data=await response.json();
        return data;
    } catch (error) {
        console.error("There was an error!",error);
    }
}
