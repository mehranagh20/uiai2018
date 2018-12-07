cmake_minimum_required(VERSION 3.10)
project(cpp)

set(CMAKE_CXX_STANDARD 11)

add_executable(cpp
        ball.cpp
        ball.h
        game.cpp
        game.h
        main.cpp
        player.cpp
        player.h
        pos.cpp
        pos.h
        strategy.cpp
        strategy.h
        team.cpp
        team.h
        triple.cpp
        triple.h)
