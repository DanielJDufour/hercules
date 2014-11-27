//disables the submit button until all the inputs have been given a value (e.g., been filled in)
$(document).ready(function(){

    var inputs = $("input");
    var submit = $("#submit");

    function controlSubmit(){
        var enable = true;

        for (var i = 0; i < inputs.length; i++)
        {
            var input = inputs[i];
            if (input.value.length === 0)
            {
                enable = false;
                break;
            }
        }
        if (enable)
        {
            submit.attr("type", "submit");
        }
        else
        {
            submit.attr("type", "button");
        } 
    }
    inputs.keyup(function(){controlSubmit();});
    controlSubmit();
});
