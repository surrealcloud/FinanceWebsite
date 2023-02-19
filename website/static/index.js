function deleteItem (itemID) {
    fetch('/delete-item', {
        method: 'POST',
        body: JSON.stringify({itemID: itemID})
    }).then((_res) => {
        window.location.href = "/budget";
    });
}