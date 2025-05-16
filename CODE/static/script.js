$(document).ready(function () {

    $('#predictionForm').submit(function (event) {
        event.preventDefault(); 


        var formData = $(this).serialize();


        $.ajax({
            url: '/prediction/y_predict', 
            type: 'POST',
            data: formData,
            success: function (response) {

                $('.prediction-result').html('<h4><span style="color: red;">' + response.prediction_text + '</span></h4>');
            },
            error: function () {

                $('.prediction-result').html('<h4><span style="color: red;">An error occurred. Please try again.</span></h4>');
            }
        });
    });
});
