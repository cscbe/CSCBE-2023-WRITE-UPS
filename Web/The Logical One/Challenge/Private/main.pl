:- module(main, []).

:- use_module(library(crypto)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_log)).
:- use_module(library(http/http_parameters)).
:- use_module(library(http/http_json)).

:- use_module(team_session).

:- set_setting(http:logfile, '/dev/stdout').

:- http_handler(root(Session/app)         , session(Session, http_reply_file('index.html', []))            , []                                    ).
:- http_handler(root(Session/api/register), session(Session, main:register(Session))                       , []                                    ).
:- http_handler(root(Session/api/login)   , session(Session, main:login(Session))                          , []                                    ).
:- http_handler(root(Session/api/action)  , session(Session, main:auth(Session, main:api(Method, Session))), [method(Method), methods([get, post])]).

:- initialization main.

main :- http_server(http_dispatch, [port(5000)]), repeat, sleep(1), fail.

register(Session, Request) :-
  http_parameters(Request, [user(User, [optional(false)])]),
  (read_term_from_atom(User, user(Name, Password), [syntax_errors(quiet)]) ->
    % If username is already used, Fail.
    (team_session_assertz(Session, user(Name, _)) -> 
      reply_json(json([status=failed, message='Username already taken']))
      ;
      % User can be registered.
      crypto_password_hash(Password, Hash),
      asserta(team_session_assertz(Session, user(Name, Hash))),
      reply_json(json([status=success, message='User created']))
    )
    ;
    % Input broke the parsing, They should not use single quotes.
    reply_json(json([status=failed, message='Invalid format. No single quotes should be used!']))
  ).

login(Session, Request) :-
  http_parameters(Request, [user(User, [optional(false)])]),
  (read_term_from_atom(User, user(Name, Password), [syntax_errors(quiet)]) ->
    % If user not exists or passwords doesn't match, Fail.
    ((team_session_assertz(Session, user(Name, Hash)),
      nonvar(Password), nonvar(Hash),
      crypto_password_hash(Password, Hash)) -> 
      % Login the user by creating a session.
      uuid(UUID, [version(4)]),
      asserta(team_session_assertz(Session, session(Name, UUID))),
      reply_json(json([status=success, message='Logged in!', session_uuid=UUID]))
      ;
      reply_json(json([status=failed, message='Incorrect username or password']))
    )
    ;
    % Input broke the parsing, They should not use single quotes.
    reply_json(json([status=failed, message='Invalid format. No single quotes should be used!']))
  ).

auth(Session, Handler, Request) :-
  member(cookie(Cookies), Request),
  member(session=SessionCookie, Cookies),
  % Check if session exists.
  team_session_assertz(Session, session(Name, SessionCookie)),
  call(Handler, [user(Name) | Request]).

api(get, Session, Request) :-
  member(user(Name), Request),

  http_parameters(Request, [item(Item, [optional(false)])]),
  (
    read_term_from_atom(Item, ItemAtom, [syntax_errors(quiet)]),
    atom(ItemAtom),

    % All saved data has 2 fields.
    functor(ItemTerm, ItemAtom, 2),
    % The first argument ("field") should be the user.
    arg(1, ItemTerm, Name),
    % Find all values of the required item.
    findall(Value, (team_session_assertz(Session, ItemTerm), arg(2, ItemTerm, Value)), Values)
    ->
    % Return the found values.
    reply_json(json([status=success, values=Values]))
    ;
    reply_json(json([status=success, values=[]]))
  ).

api(post, Session, Request) :-
  http_parameters(Request, [item(Item, [optional(false)])]),
  (
    read_term_from_atom(Item, ItemTerm, [syntax_errors(quiet)]),
    % No free variables in Item.
    ground(ItemTerm),
    % Save Item.
    asserta(team_session_assertz(Session, ItemTerm))
    ->
    reply_json(json([status=success, message='Item has been saved']))
    ;
    reply_json(json([status=failed, message='Failed to save the item. Probably malformed.']))
  ).