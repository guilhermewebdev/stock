import connect from '@/connect';
import { Method } from 'axios';

async function iterate(list:Array<any>, callback:Function, start:number=0):Promise<void>{
    callback(list[start], start)
    start++
    return list[start]? iterate(list, callback, start) : undefined;
}

async function iterateJSON(json:any, callback:Function){
    iterate(Object.keys(json), function(key:string) {
        callback(json[key], key)
    })
}

interface Credentials {
    username?:string;
    email?:string;
    password:string;
}

interface Reactive {
    observers:Array<Function>;
    notifyObservers:Function;
    addObserver:Function;
    resetObservers:Function;
}

interface Hierarchy {
    father?:CRUD;
    addChild:Function;
    addMultipleChilds:Function;
}

interface CRUD extends Hierarchy, Reactive {
    list?:Array<any>;
    url?:string;
    item?:any;
    selected?:number;
    key:string;
    haveItems:boolean;
    loadList:Function;
    getURL:Function;
    loadItem:Function;
    getURLItem:Function;
    createItem:Function;
    deleteItem:Function;
    updateItem:Function;
    partialUpdateItem:Function;
    getItem:Function;
}

async function request(method:Method, url:string, data?:any):Promise<any>{
    return new Promise((accept, reject) => {
        connect(url, {
            method:method,
            data:data,
        })
            .then(response => accept(response.data))
            .catch(reject)
    })
}

const reaction:Reactive = {
    observers: [],
    async notifyObservers(){
        iterate(this.observers, (observer:Function) => {
            if(observer) observer(this)
        })
        if('father' in this) this.father.notifyObservers()
    },
    async addObserver(observer:Function){
        this.observers.push(observer)
    },
    async resetObservers(){
        this.observers = []
    }
}

const hiearachy:Hierarchy = {
    async addChild(child:CRUD, name:string){
        Object.defineProperty(child, 'father', {
            value: this
        })
        Object.defineProperty(this, name, {
            value: child,
        })
    },
    async addMultipleChilds(childs:JSON){
        iterateJSON(childs, (item:CRUD|Hierarchy, key:string) => {
            this.addChild(item, key);
        })
    }
}

const crud:CRUD = {
    ...hiearachy,
    ...reaction,
    haveItems: true,
    key: 'pk',
    list: [],
    async loadList(){
        return request('GET', this.getURL('/?format=json'))
            .then((data:Array<any>) => {
                this.list = data
                this.notifyObservers()
            })
    },
    getURL(sufix:string = ''){
        if(this.father){
            return `${this.father.getURLItem()}${this.url}${sufix}`
        }else{
            return `${this.url}${sufix}`
        }
    },
    getURLItem(item?:number, sufix:string = ''){
        if(this.father){
            if(this.haveItems){
                if(this.selected && !item){            
                    return `${this.father.getURLItem()}${this.url}/${this.selected}${sufix}`
                }else if(item){
                    return `${this.father.getURLItem()}${this.url}/${item}${sufix}`
                }else throw new Error('É preciso selecionar um item')
            }else{
                return `${this.father.getURLItem()}${this.url}${sufix}`
            }
        }else {
            if(this.haveItems){
            alert(this)
                if(this.selected && !item){            
                    return `${this.url}/${this.selected}${sufix}`
                }else if(item){
                    return `${this.url}/${item}${sufix}`
                }else throw new Error('É preciso selecionar um item')
            }else{
                return `${this.url}${sufix}`
            }
        }
    },
    async loadItem(item:number){
        return request('GET', this.getURLItem(item))
            .then((data:any) =>{
                this.item = data
                this.key = this.item[this.key];
                this.notifyObservers()
            })
    },
    async getItem(item:number){
        return new Promise((accept, reject) => {
            if(this.list){
                iterate(this.list, (item:any) => {
                    if(item[this.key] === item) accept(item)
                })
                this.notifyObservers()
            }else{
                this.loadItem(item).then(accept).catch(reject)
            }
        });
    },
    async createItem(data:any){
        return request('POST', this.getURL('/?format=json'), data)
            .then((data:any) => {
                this.list.push(data)
                this.notifyObservers()
            });
    },
    async deleteItem(item:number){
        return request('DELETE', this.getURLItem(item, '/?format=json'))
            .then(re => {
                this.loadList()
                this.notifyObservers()
            })
    },
    async updateItem(item:number, data:any){
        return request('PUT', this.getURLItem(item, '/?format=json'), data)
            .then(re => {
                this.loadList()
                this.notifyObservers()
            })
    },
    async partialUpdateItem(item:number, data:any){
        return request('PATCH', this.getURLItem(item, '/?format=json'), data)
            .then(re => {
                this.loadList()
                this.notifyObservers()
            })
        
    },
}

const app:CRUD|any = {
    ...crud,
    haveItems: false,
    url: 'http://localhost/api',
    async mount(){
        this.sessions.checkAuth()
    }
}

app.addChild({
    ...crud,
    async login(credentials:Credentials){
            return request('POST', this.getURL('/login/?format=json'), credentials)
                .then(re => {
                    this.isAuthenticated = true;
                    this.checkAuth()
                })
    },
    async logout(){
        return new Promise((accept, reject) => {
            return request('DELETE', this.getURL('/logout/?format=json'))
                .then(re => {
                    this.isAuthenticated = false;
                    this.user = {};
                    accept(re)
                    this.notifyObservers()
            })
                .catch(reject)
        })
    },
    async register(user:any){
        return request('POST', this.getURL(`/registration/?format=json`), user)
            .then(re => this.notifyObservers())
    },
    async checkAuth(){
        return request('GET', this.getURL('/user/?format=json'))
            .then(user => {
                this.isAuthenticated = true;
                this.user = user;
                this.notifyObservers()
            })
    },
    isAuthenticated: false,
    user: {},
    url: '/sessions',
    haveItems: false,
}, 'sessions')

app.sessions.addChild({
    async reset(data:any){
        return request('POST', this.getURL('/reset/?format=json'), data)
    },
    async change(data:any){
        return request('POST', this.getURL('/change/?format=json'), data)        
    },
    url: '/password',
    ...crud,
    haveItems: false,
}, 'password')

app.sessions.addChild({
    ...crud,
    haveItems: false,
    url: '/user'
}, 'user')

app.addMultipleChilds({
    products: {
        ...crud,
        url: '/products'
    },
    categories: {
        ...crud,
        url: '/categories'
    },
    requests: {
        ...crud,
        url: '/requests'
    },
    purchases: {
        ...crud,
        url: '/purchases'
    },
    removals: {
        ...crud,
        url: '/removals'
    },
    consumers: {
        ...crud,
        url: '/consumers',
    },
    deliveries: {
        ...crud,
        url: '/deliveries'
    }
})

app.requests.addChild({
    ...crud,
    url: '/consum'
}, 'consum')

app.products.addChild({
    ...crud,
    url: '/additions'
}, 'additions')

app.categories.addChild({
    ...crud,
    url: '/products'
}, 'products')

export default app;