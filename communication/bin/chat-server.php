<?php

/**
 * To install ratchet socket stuffs:
 * https://getcomposer.org/download/
 * http://socketo.me/docs/install
 * http://socketo.me/docs/hello-world
 * php composer.phar update
 */

use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;
use MyApp\Chat;

    require dirname(__DIR__) . '/vendor/autoload.php';

    $server = IoServer::factory(
        new HttpServer(
            new WsServer(
                new Chat()
            )
        ),
        8080
    );

    $server->run();

?>