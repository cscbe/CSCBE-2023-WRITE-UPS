:- module(team_session, [
  team_session/1,
  team_session_assertz/2,

  session/3
]).

:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_json)).
:- use_module(library(base64)).
:- use_module(library(crypto)).

:- http_handler(root('.'), http_reply_file('team_session_create.html', []), []).
:- http_handler(root(create_team_session), create_team_session, [method(post)]).

:- dynamic([team_session/1, team_session_assertz/2], [multfile(true)]).

create_team_session(_Request) :-
  getenv('CHALL_PWD', Pwd),
  getenv('CHALL_FLAG', Flag),

  uuid(UUID, [version(4)]),
  asserta(team_session(UUID)),
  
  % Assert admin user in session.
  crypto_password_hash(Pwd, Hash),
  asserta(team_session_assertz(UUID, user(admin, Hash))),

  % Assert admin note containg flag in session.
  % The application expects notes to be base64 encoded.
  base64_encoded(Flag, Encoded, [as(atom)]),
  asserta(team_session_assertz(UUID, note(admin, Encoded))),

  reply_json(json([team_session=UUID])).

session(Session, Handler, Request) :-
  (team_session(Session) ->
    call(Handler, Request)
    ;
    call(http_redirect(moved_temporary, root(.)), Request)
  ).