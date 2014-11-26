$(document).ready(function(){

    function searchRows(){
        console.log("starting searchRows");
        var sval = document.getElementById("search").value;
        var rows = $("tbody tr");

        if (sval.length === 0)
        {
            rows.show();
        }
        else
        {
            terms = sval.toUpperCase().trim().split(" ");
            console.log("terms are " + terms.toString());
            for (var r = 0; r < rows.length; r++)
            {
                var row = rows[r];
                var rowjq = $(row);
                console.log("rowjq is:");
                console.log(rowjq);
                var textContent = row.textContent.toUpperCase();
                console.log("textContent is " + textContent);
                var match = true;
                for (var t = 0; t < terms.length; t++)
                {
                    if (textContent.indexOf(terms[t]) == -1)
                    {
                        match = false;
                        break;
                    }
                }
                if (match)
                {
                    rowjq.show();
                }
                else
                {
                    rowjq.hide();
                }
            }
        }
    } //end searchRows()

    $("#search").keyup(function(){searchRows();});
});
