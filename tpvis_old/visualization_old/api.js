export function request_layout(request_json){
    return fetch("http://localhost:5000/compute_layout", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request_json)
    })
    .then(response=>{
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json(); 
    })
    .catch(error => {
        console.error("API 요청 실패:", error);
        throw error; 
    });
}


