
FROM php:5.4-cli

ADD php.ini /usr/local/etc/php
ADD test.php /home/

ADD libwebshell.so /usr/local/lib/php/extensions/no-debug-non-zts-20100525/

CMD php -f /home/test.php
