$(document).ready(function(){
	"use strict";

	var window_width 	 = $(window).width(),
	window_height 		 = window.innerHeight,
	header_height 		 = $(".default-header").height(),
	header_height_static = $(".site-header.static").outerHeight(),
	fitscreen 			 = window_height - header_height;


	$(".fullscreen").css("height", window_height)
    $(".fitscreen").css("height", fitscreen);

  //------- Active Nice Select --------//

    $('select').niceSelect();


    $('.navbar-nav li.dropdown').hover(function() {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
    }, function() {
    $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
    });

    $('.img-pop-up').magnificPopup({
        type: 'image',
        gallery:{
        enabled:true
        }
    });

    // Search Toggle
    $("#search_input_box").hide();
    $("#search").on("click", function () {
        $("#search_input_box").slideToggle();
        $("#search_input").focus();
    });
    $("#close_search").on("click", function () {
        $('#search_input_box').slideUp(500);
    });

   /*==========================
		javaScript for sticky header
		============================*/
    $(".sticky-header").sticky();

    /*=================================
    Javascript for banner area carousel
    ==================================*/
    $(document).ready(function() {
        if ($('.active-banner-slider').children().length > 0) {
            $('.active-banner-slider').owlCarousel({
                items: 1,
                autoplay: false,
                loop: true,
                nav: true,
                navText: ["<img src='/static/img/banner/prev.png'>", "<img src='/static/img/banner/next.png'>"],
                dots: false
            });
        } else {
            console.log("Карусель баннеров пуста!");
        }
    });

    /*=================================
    Javascript for product area carousel
    ==================================*/
    if ($('.active-banner-slider').children().length > 0) {
      $('.active-banner-slider').owlCarousel({
         items: 1,
         loop: true,
         autoplay: true,
         nav: true,
         navText:["<img src='/static/img/product/prev.png'>","<img src='/static/img/product/next.png'>"],
         dots:false
      });
    };

    /*=================================
    Javascript for single product area carousel
    ==================================*/
    $(".s_Product_carousel").owlCarousel({
        items: 1,
        loop: true,
        dots: true,
        nav: false,
        touchDrag: true,    // Для сенсорных устройств
        mouseDrag: true,     // Включаем перетаскивание мышью
        pullDrag: true,      // Добавляем для лучшей совместимости
        autoplay: false
    });

    /*=================================
    Javascript for exclusive area carousel
    ==================================*/
    $('.product-carousel').owlCarousel({
        items: 1, // Показывать по одному слайду
        loop: true,
        nav: true,
        dots: false,
        autoplay: false,
        navText:["<img src='/static/img/product/prev.png'>","<img src='/static/img/product/next.png'>"],
    });

    $(".active-exclusive-product-slider").owlCarousel({
        items:1,
        autoplay:false,
        autoplayTimeout: 5000,
        loop:true,
        nav:true,
        navText:["<img src='/static/img/product/prev.png'>","<img src='/static/img/product/next.png'>"],
        dots:false
    });

    //--------- Accordion Icon Change ---------//

    $('.collapse').on('shown.bs.collapse', function(){
        $(this).parent().find(".lnr-arrow-right").removeClass("lnr-arrow-right").addClass("lnr-arrow-left");
    }).on('hidden.bs.collapse', function(){
        $(this).parent().find(".lnr-arrow-left").removeClass("lnr-arrow-left").addClass("lnr-arrow-right");
    });

  // Select all links with hashes
  $('.main-menubar a[href*="#"]')
    // Remove links that don't actually link to anything
    .not('[href="#"]')
    .not('[href="#0"]')
    .click(function(event) {
      // On-page links
      if (
        location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
        &&
        location.hostname == this.hostname
      ) {
        // Figure out element to scroll to
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        // Does a scroll target exist?
        if (target.length) {
          // Only prevent default if animation is actually gonna happen
          event.preventDefault();
          $('html, body').animate({
            scrollTop: target.offset().top-70
          }, 1000, function() {
            // Callback after animation
            // Must change focus!
            var $target = $(target);
            $target.focus();
            if ($target.is(":focus")) { // Checking if the target was focused
              return false;
            } else {
              $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
              $target.focus(); // Set focus again
            };
          });
        }
      }
    });

      $('.quick-view-carousel-details').owlCarousel({
          loop: true,
          dots: true,
          items: 1,
      })

    //----- Active No ui slider --------//



    $(function() {
      $('input[name="name"]').on('input', function() {
        if ($(this).val()) {
          $(this).addClass('has-value');
        } else {
          $(this).removeClass('has-value');
        }
      });
    });

//    $(function() {
//      if(document.getElementById("price-range")) {
//        var nonLinearSlider = document.getElementById('price-range');
//
//        noUiSlider.create(nonLinearSlider, {
//            connect: true,
//            behaviour: 'tap',
//            start: [ 500, 4000 ],
//            range: {
//                'min': [ 0 ],
//                '10%': [ 500, 500 ],
//                '50%': [ 4000, 1000 ],
//                'max': [ 10000 ]
//            }
//        });
//
//        var nodes = [
//            document.getElementById('lower-value'), // 0
//            document.getElementById('upper-value')  // 1
//        ];
//
//        // Display the slider value and how far the handle moved
//        // from the left edge of the slider.
//        nonLinearSlider.noUiSlider.on('update', function ( values, handle, unencoded, isTap, positions ) {
//            nodes[handle].innerHTML = values[handle];
//            $("#lower-value").val(values[0]);
//            $("#upper-value").val(values[1]);
//        });
//      }
//    });


    //-------- Have Cupon Button Text Toggle Change -------//

    $('.have-btn').on('click', function(e){
        e.preventDefault();
        $('.have-btn span').text(function(i, text){
          return text === "Have a Coupon?" ? "Close Coupon" : "Have a Coupon?";
        })
        $('.cupon-code').fadeToggle("slow");
    });

    $('.load-more-btn').on('click', function(e){
        e.preventDefault();
        $('.load-product').fadeIn('slow');
        $(this).fadeOut();
    }); 
});


document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const hiddenInput = document.getElementById('id_star');

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const value = this.dataset.value;
            hiddenInput.value = value;

            // Обновляем визуальное отображение
            stars.forEach(s => {
                s.classList.remove('active');
                if (s.dataset.value <= value) {
                    s.classList.add('active');
                }
            });
        });

        star.addEventListener('mouseover', function() {
            const hoverValue = this.dataset.value;
            stars.forEach(s => {
                s.classList.remove('active');
                if (s.dataset.value <= hoverValue) {
                    s.classList.add('active');
                }
            });
        });

        star.addEventListener('mouseout', function() {
            const currentValue = hiddenInput.value || 0;
            stars.forEach(s => {
                s.classList.remove('active');
                if (s.dataset.value <= currentValue) {
                    s.classList.add('active');
                }
            });
        });
    });
});

if(document.getElementById("js-countdown")){
    var countdownDate = new Date("March 07, 2025 00:00:00");

    function getRemainingTime(endtime) {
        var total = Date.parse(endtime) - Date.parse(new Date());
        var seconds = Math.floor((total / 1000) % 60);
        var minutes = Math.floor((total / 1000 / 60) % 60);
        var hours = Math.floor((total / (1000 * 60 * 60)) % 24);
        var days = Math.floor(total / (1000 * 60 * 60 * 24));

        return {
            'total': total,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        };
    }

    function initClock(id, endtime) {
        const counter = document.getElementById(id);
        if (!counter) {
            console.error('Элемент с id ' + id + ' не найден!');
            return;
        }

        var daysItem = counter.querySelector('.js-countdown-days');
        var hoursItem = counter.querySelector('.js-countdown-hours');
        var minutesItem = counter.querySelector('.js-countdown-minutes');
        var secondsItem = counter.querySelector('.js-countdown-seconds');

        // Проверка всех элементов
        if (!daysItem || !hoursItem || !minutesItem || !secondsItem) {
            console.error('Не найдены элементы таймера!');
            return;
        }

        function updateClock() {
            const t = getRemainingTime(endtime);

            daysItem.textContent = t.days;
            hoursItem.textContent = ('0' + t.hours).slice(-2);
            minutesItem.textContent = ('0' + t.minutes).slice(-2);
            secondsItem.textContent = ('0' + t.seconds).slice(-2);

            if (t.total <= 0) {
                clearInterval(timeinterval);

                // Проверка существования кнопки
                const buyButton = document.querySelector('.buy-button');
                if (buyButton) {
                    buyButton.disabled = true;
                } else {
                    console.warn('Кнопка .buy-button не найдена!');
                }

                counter.innerHTML = '<div class="smalltext promo-ended">Время вышло!</div>';
                document.querySelector('.buy-button').disabled = true; // Блокировка кнопки
            }
        }

        updateClock(); // Первоначальный запуск
        var timeinterval = setInterval(updateClock, 1000);
    }

    initClock('js-countdown', countdownDate);
}
