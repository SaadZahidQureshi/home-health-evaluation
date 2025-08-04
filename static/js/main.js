(function ($) {

    $(document).ready(function () {

        // Hamburger-menu
        $('.hamburger-menu').on('click', function () {
            $('.hamburger-menu .line-top, .main-left-col, .right-mainpart').toggleClass('current');
            $('.hamburger-menu .line-center').toggleClass('current');
            $('.hamburger-menu .line-bottom').toggleClass('current');
        });


        // accordian ----------
        $(".accordian_cnt").click(function() {
            $(this).toggleClass("active").next().slideToggle();
        });



    });

})(jQuery);
