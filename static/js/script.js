$(document).ready(function() {

    post_action = () => {
        $('.post .right-info img').click(function() {
            $('.menu-actions').css({ display: 'none' })
            $(this).next().css({ display: 'flex' });

        });

        $(window).click(function(event) {
            if (!$(event.target).is(".post .right-info img")) {
                $('.menu-actions').css({ display: 'none' })
            }
        });
    }
    post_action();




    var hide = true
    var input_pass = $('.content input[type="password"]');
    var hide_icon = $('.content .form_control img');


    $('.content input').focusout(function(e) {
        e.preventDefault();

        if ($(this).val() != '') {
            $(this).parent().addClass('has-data')
        } else {
            $(this).parent().removeClass('has-data')

        }

    });


    $.each(hide_icon, function(i, v) {
        $(this).click(function(e) {
            e.preventDefault();
            if (hide == true) {
                $(input_pass[i]).attr('type', 'text');
                $(input_pass[i]).css({ 'background-image': ' url(/static/images/icons8-password.svg' })
                $(hide_icon[i]).attr('src', '/static/images/icons8-show-24.png')
                hide = false

            } else {
                $(input_pass[i]).attr('type', 'password');
                $(hide_icon[i]).attr('src', '/static/images/icons8-hide-30.png')
                hide = true
            }

        });
    });


    $('.first_page .next ,.first_page .skip').click(function(e) {
        e.preventDefault();
        $(this).parent().css({ 'transform': 'translateX(365px)', 'transition': '0.2s all ease-in-out' })
        $('.second_page').css({ 'transform': 'translateX(400px)', 'transition': '0.2s all ease-in-out' })


    });
    $('.second_page .next , .second_page .skip').click(function(e) {
        e.preventDefault();
        $(this).parent().css({ 'transform': 'translateX(365px)', 'transition': '0.2s all ease-in-out' })
        $('.third_page').css({ 'transform': 'translateX(-400px)', 'transition': '0.2s all ease-in-out' })


    });


    $('.close-alert').click(function() {
        $(this).parent().css({ transform: 'translateY(-100px)' })
    })
    $('.new_post .cancel').click(function() {
        $('.new_post').css({ 'transform': 'scale(0)' })
        $('.main .overlay').addClass('hide');

    });
    $('.side-content .create_post').click(function() {

        $('.new_post #create-post').attr('value', 'Post')
        $('.new_post').css({ 'transform': 'scale(1)' })


    })
    const post_photo_input = document.querySelector('.new_post input[type=file] ');
    const post_photo = document.querySelector('.new_post .post_image ');

    post_photo_input.addEventListener('change', () => {
        if (post_photo_input.files && post_photo_input.files[0]) {
            $('.cont_post-image').removeClass('hide');
            $('.cont_post-image .close').addClass('hide');
            $(post_photo).css({ width: '75px', height: '90px' });
            $('.cont_post-image').css({ display: 'flex', justifyContent: 'center', alignItems: 'center' });
            $(post_photo).attr('src', "/static/images/spinner.gif");
            setTimeout(function() {
                $('.cont_post-image .close').removeClass('hide');
                $(post_photo).css({ width: '100%', height: '250px' });
                post_photo.src = URL.createObjectURL(post_photo_input.files[0]);
                $('.cont_post-image').removeClass('hide');
            }, 500)
        }
    });


});