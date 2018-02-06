# python-graphql-lesson
A Little Demo for G9 Python Talks Showing off GraphQL and Graphene

# What is GraphQL?
GraphQL is a data querying language developed by Facebook. It was created as an alternative to traditional REST and ad-hoc webservice frameworks. When using GraphQL, clients send requests that define the structure of the data they want returned. The data is then returned in the same structure sent by the client. It's strong typing helps avoid the issues of under- and over-fetching data. 

# What does GraphQL really look like?

For example, we could define a type:

```
type Node {
    title: String
    nid: Int
    tags: [String]
}
```

And using this type, we can write a query:

```
{
    node(name: "Ice Beer Article") {
        nid
        tags
    }
}
```

And then you'll get back pretty predictable data (in a predictable format):

```
{
    "node": {
        "nid": 4052115,
        "tags": ["Ice Beer", "bur", "chill", "v chill", "much frío"]
    }
}
```

# Cool, so how do we define types?
Defining types is pretty simple in GraphQL. For example, let's say we wanted to define a Node type. A node is an object with a title, node id (which we'll call `nid`), a field `is_published` that determines if a node is published, and a list of tags, unimaginatively called `tags`. We can define this type in a pretty straightforward manner:

```
type Node {
    title: String!
    nid: Int!
    is_published: Boolean!
    tags: [Tag]!
}
```

The above example demonstrates how easy it is to read GraphQL schemas. The Node type in our schema defines a non-null `title` field (the non-null is denoted by the `!`, a non-null `nid` field, a non-null `is_published` boolean field, and a list of at least zero or more tag objects.) 

## The Query and Mutation Types
While most types in your schema will be normal objects, there are two special types: Query and Mutation.

### The Query Type
_Every_ GraphQL schema will have a Query type. The fields of the Query type denote the entry points for querying (only) within your schema. For example, if we have the query:

```
query {
    node(nid: 4052115) {
        title
        tags
    }
    tags(tid: 1937) {
        title
    }
}
```

That _*must*_ mean that we defined our Query type in the following way:

```
type Query {
    node(nid: Int): Node
    tags(tid: Int): Tag
}
```

This means that there is a `node` entrypoint that can take a `nid` parameter and return some `Node`s, in addition to a `tags` entrypoint that takes in an optional `tid` parameter and returns `Tag` objects.

### The Mutation Type
The mutation type works essentially the same way as the query type.

### Interfaces
Much like in OOP contexts, you can also define interfaces that force your types to have some predefined fields. For example, we can define an Entity interface like so:

```
interface Entity {
    entity_id: ID!
    title: String!
}
```

And then we can have our types in the schema _implement_ that interface:

```
type Node implements Entity {
    entity_id: ID!
    title: String!
    is_published: Boolean!
    tags: [Tag]!
    summary: String
}

type Tag implements Entity {
    entity_id: ID!
    title: String!
    tag_mobile_title: String
}
```

Notice how both the `Node` and `Tag` types have `entity_id` and `title` defined. Each type is also allowed to define type-specific fields, like `is_published` for nodes and `tag_mobile_title` for tags. 

# And how do we query those types?
Writing queries in GraphQL is pretty simple as well. Let's say we want to find the title and tags for a list of articles. We can write the following query given how we've developed our schema so far:

```
query {
    node {
        title
        summary
        entity_id
    }
}
```

This is a pretty simple query that'll return the entity ID, title, and summary of the list of nodes we have. However, let's say we add another entrypoint in our schema that allows us to find entity titles:

```
type Query {
    ...
    entityById(entity_id: ID!): Entity
}
```

The above entrypoint would return `Node`s and `Tag`s. Because the return type is `Entity`, we can't necessarily write a query like the following:

```
query {
    entityById(entity_id: 4052115) {
        title
        is_published
        tags
    }
}
```

This is because the Entity interface doesn't define the `is_published` and `tags` fields (even if one of its implementors has them). However, we can use _fragments_ to conditionally select fields to include in our response based on type. For example:

```
query {
    entityById(entity_id: 4052115) {
        title
        ... on Node {
            is_published
            tags
        }
        ... on Tag {
            tag_mobile_title
        }
    }
}
```

This will always display the title for whatever entity is fetched, THEN it will display either the published status and list of tags if it's a node or the mobile title for the tag if it's a tag. We can also name fragments like so:

```
fragment nodeFields on Node {
    is_published
    tags
}

fragment tagFields on Tag {
    tag_mobile_title
}
```

# Serving GraphQL over HTTP

So how do we _actually_ use GraphQL in a production environment? To start, the server needs to use [a framework, library, or the sort](http://graphql.org/code/) to define their schema and types. The big difference between GraphQL and REST architectures are the endpoints. GraphQL traditionally uses one endpoint (e.g. https://cms.thrillist.com/graphql) that takes all of the queries. Entrypoints defined in the `Query` object should be made with GET requests, whereas entrypoints defined in a `Mutation` object should be made as a `POST` request with either content header type `application/json` or `application/graphql`. 

An example request might look like: 
`http://cms.thrillist.com/graphql?query={node(nid: 4052115){title}}` via HTTP GET. 

# Running the Sample GraphQL Demo
You'll notice in this repository some set up to create a docker container (and a `requirements.txt` file if you prefer virtualenv). Run the following commands and head over to `localhost:8080/graphql` to play around with the interactive environment. Note that there is no data included by default, so you'll need to add data on your own. 