<template>
    <v-app>
        <v-main>
            <HelloWorld/>
        </v-main>
    </v-app>
</template>

<script>
    import HelloWorld from './components/OptionsAI';

    export default {
        name: 'App',

        components: {
            HelloWorld,
        },

        data: () => ({
            //
        }),


    };
</script>
