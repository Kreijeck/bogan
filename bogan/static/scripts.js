function scroll_table(maxRows) {
    
    //window.alert("Die maximale Anzahl ist: " + maxRows)

    var table = document.getElementById('id_scroll');
    var wrapper = table.parentNode;
    var rowsInTable = table.rows.length;
    var height = 0;
    if (rowsInTable > maxRows) {
        for (var i = 0; i < maxRows; i++) {
            height += table.rows[i].clientHeight;
        }
        wrapper.style.height = height + "px";
        wrapper.style.width = "100%";
    }
}
