function updateRequest(id, action) {
    fetch(`/api/request/${id}/action?action=${action}`, { method: "POST" })
        .then(response => response.json())
        .then(data => {
            alert(`Заявка ${id} ${action}`);
            location.reload();
        });
}
