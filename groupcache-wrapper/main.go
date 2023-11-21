package main

import (
	"context"
	"errors"
	"log"
	"net/http"

	"github.com/golang/groupcache"
)

import "C"

// temporary storage to be able to set data
var Store = map[string]string{}

var peers *groupcache.HTTPPool = nil
var cache *groupcache.Group = nil
var srv *http.Server = nil

//export cache_set
func cache_set(key *C.char, value *C.char) *C.char {
	// set the value in the cache.

	// groupcache does not have a way to set a value in the cache (pass through cache),
	// so we fake it by setting value in global store and then getting the value immediately.
	// Ideally, this is switched out with a backend that retrieves the value you want to cache.
	var gkey = C.GoString(key)
	var gvalue = C.GoString(value)
	Store[gkey] = gvalue
	var data string
	cache.Get(context.TODO(), gkey, groupcache.StringSink(&data))
	delete(Store, gkey)
	return C.CString(data)
}

//export cache_get
func cache_get(key *C.char) *C.char {
	// get the value from the cache.
	var data string
	cache.Get(context.TODO(), C.GoString(key), groupcache.StringSink(&data))
	return C.CString(data)
}

//export setup
func setup(addr *C.char, baseUrl *C.char) {
	// setup the cache server.
	done := make(chan bool)
	go func() {
		log.Printf("Setting up cache server node at %s...\n", C.GoString(addr))
		peers = groupcache.NewHTTPPool(C.GoString(baseUrl))
		cache = groupcache.NewGroup("Cache", 64<<20, groupcache.GetterFunc(
			func(ctx groupcache.Context, key string, dest groupcache.Sink) error {
				v, ok := Store[key]
				if !ok {
					return errors.New("cache key not found")
				}
				dest.SetBytes([]byte(v))
				return nil
			}))
		router := http.NewServeMux()
		router.Handle("/", http.HandlerFunc(peers.ServeHTTP))
		srv := &http.Server{Addr: C.GoString(addr), Handler: router}
		close(done)
		if err := srv.ListenAndServe(); err != nil {
			log.Fatal("ListenAndServe: ", err)
		}
	}()
	<-done
	// do it in a go routine so we don't block
	log.Printf("Running cache server node at %s.\n", C.GoString(addr))
}

//export initialized
func initialized() *C.char {
	// check if cache is initialized. If it is, then we can use it.
	var flag string
	if cache != nil {
		flag = "1"
	} else {
		flag = "0"
	}
	return C.CString(flag)
}

func main() {}
