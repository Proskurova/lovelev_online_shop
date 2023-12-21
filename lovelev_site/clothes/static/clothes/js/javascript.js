// Для popup

const popupLinks = document.querySelectorAll('.popup-link');
const  body = document.querySelector('body');
const  lockPadding = document.querySelectorAll('.lock-padding');

let unlock = true;

const timeout = 800;

if (popupLinks.length > 0) {
    for (let index = 0; index < popupLinks.length; index++) {
        const popupLink = popupLinks[index];
        popupLink.addEventListener("click", function (e) {
            const popupName = popupLink.getAttribute('href').replace('#', '');
            const curentPopup = document.getElementById(popupName);
            popupOpen(curentPopup);
            e.preventDefault();
        });
    }
}
const popupCloseIcon = document.querySelectorAll('.close-popup');
if (popupCloseIcon.length > 0) {
    for (let index = 0; index < popupCloseIcon.length; index++) {
        const el = popupCloseIcon[index];
        el.addEventListener("click", function (e) {
            popupClose(el.closest('.popup'));
            e.preventDefault()
        });
    }
}

function popupOpen(curentPopup) {
    if (curentPopup && unlock) {
        const popupActive = document.querySelector('.popup.open');
        if (popupActive) {
            popupClose(popupActive, false);
        } else {
            bodyLock();
        }
        curentPopup.classList.add('open');
        curentPopup.addEventListener("click", function (e) {
            if (!e.target.closest('.popup_content')) {
                popupClose(e.target.closest('.popup'));
            }
        });
    }
}
function popupClose(popupActive, doUnlock = true) {
    if (unlock) {
        popupActive.classList.remove('open');
        if (doUnlock) {
            bodyUnLock();
        }
    }
}

function bodyLock() {
    const lockPaddingValue = window.innerWidth - document.querySelector('.wrapper').offsetWidth + 'px';

    if (lockPadding.length > 0) {
        for (let index = 0; index < lockPadding.length; index++) {
            const el = lockPadding[index];
            el.style.paddingRight = lockPaddingValue;
        }
    }
    body.style.paddingRight = lockPaddingValue;
    body.classList.add('lock');

    unlock = false;
    setTimeout(function () {
        unlock = true;
    }, timeout);
}

function bodyUnLock() {
    setTimeout(function () {
        if (lockPadding.length > 0) {
            for (let index = 0; index < lockPadding.length; index++) {
                const el = lockPadding[index];
                el.style.paddingRight = '0px';
            }
        }
        body.style.paddingRight = '0px';
        body.classList.remove('lock');
    }, timeout);

    unlock = false;
    setTimeout(function () {
        unlock = true;
    }, timeout);
}

// Для меню в мобилке
let isMobile = {
	Android: function() {return navigator.userAgent.match(/Android/i);},
	BlackBerry: function() {return navigator.userAgent.match(/BlackBerry/i);},
	iOS: function() {return navigator.userAgent.match(/iPhone|iPad|iPod/i);},
	Opera: function() {return navigator.userAgent.match(/Opera Mini/i);},
	Windows: function() {return navigator.userAgent.match(/IEMobile/i);},
	any: function() {return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());}
};
		let bodyM=document.querySelector('body');
if(isMobile.any()){
		bodyM.classList.add('touch');
		let arrow=document.querySelectorAll('.header_link');
	for(i=0; i<arrow.length; i++){
			let subMenu=arrow[i].nextElementSibling;
			let thisArrow=arrow[i];

		arrow[i].addEventListener('click', function(){
			subMenu.classList.toggle('open');
			thisArrow.classList.toggle('active');
		});
	}
}else{
	bodyM.classList.add('mouse');
}

// Для меню бургер
$(document).ready(function () {
    $('.header_burger').click(function (event) {
        $('.header_burger, .header_menu').toggleClass('active_burger');
        $('body').toggleClass('lock');
    });
});

// Для листания фото
$(document).ready(function (){
    $('.photo_card_flipping').slick({
        arrows: true,
        adaptiveHeight: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        speed: 100,
        infinite: false,
    });
});

// Для форм
$(function() {
    $('#question_user_form').on('submit', function(event) {
      event.preventDefault();
      $.ajax({
        url: "http://127.0.0.1:8000/question_user_form/",
        type: 'POST',
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response) {
          if (response.success) {
              $("div.popup_text").hide();
              $('#success').html('<div class="success_text">Благодарим за проявленный интерес,<br>мы обязательно свяжемся с вами в течении суток!</div>').show();
          } else {
              // Нада поработать над этим
              $('#popup_form_question').html('<div> + response.errors + </div>').show();
          }
        }
      });
    });
  });

$(function() {
    $('#cart_form').on('submit', function(event) {
      event.preventDefault();
      $.ajax({
        url: "http://127.0.0.1:8000/orders/create/",
        type: 'POST',
        data: $(this).serialize(),
        dataType: 'json',
        success: function(response) {
          if (response.success) {
              $("div.form_cart").hide();
              $("#popup_created").html('<div class="success success_text">Ваш заказ принят! <br>Благодарим за заказ!</div>').show();
          } else {
              // Нада поработать над этим
          }
        }
      });
    });
  });
