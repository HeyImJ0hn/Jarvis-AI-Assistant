const { Client, GatewayIntentBits, SlashCommandBuilder, REST, Routes } = require('discord.js');
const fs = require('fs');

const BOT_TOKEN = '';
const GUILD_ID = '1305703618137161838';
const CLIENT_ID = '1306320288027381790';

const membersRolesData = JSON.parse(fs.readFileSync('data/paid_roles.json', 'utf8'));

console.log(`Loaded ${membersRolesData.length} members with roles data.`);

const ROLE_MAPPING = {
    "CatchCombos Client": "CatchCombos [Paid]",
    "BBottleCaps Client": "BBottleCaps [Paid]",
    "TTMs Client": "TTMs [Paid]",
    "SimpleLures Client": "SimpleLures [Paid]",
    "EntityCommands Client": "EntityCommands [Paid]",
    "PokeSell Client": "PokeSell [Paid]"
};

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMembers] });

client.once('ready', () => {
    console.log(`Bot is logged in as ${client.user.tag} and ready.`);
    updateRolesAll();
});

client.on('guildMemberAdd', async (member) => {
    updateRoles(member);
});

/*
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isCommand()) return;

    if (interaction.commandName === 'update') {
        if (!interaction.member.permissions.has('ADMINISTRATOR')) {
            await interaction.reply('You do not have permission to run this command.');
            return;
        }
        await updateRolesAll();
        await interaction.reply('Roles updated for all members.');
    }
});
*/

async function updateRolesAll() {
    const guild = client.guilds.cache.get(GUILD_ID);
    const members = await guild.members.fetch();

    for (const member of members.values()) {
        await updateRoles(member);
    }    
}

async function updateRoles(member) {
    if (member.guild.id !== GUILD_ID) return;

    console.log(`Updating roles for user ${member.displayName} (${member.id})...`);

    const userRoles = membersRolesData.find(user => user.userId === member.id)?.roles;
    if (!userRoles) {
        console.log(`No specific roles found for user ${member.displayName} (${member.id}).`);
        return;
    }

    for (const oldRoleName of userRoles) {
        const newRoleName = ROLE_MAPPING[oldRoleName];
        
        if (newRoleName) {
            const role = member.guild.roles.cache.find(r => r.name === newRoleName);
            
            if (role) {
                try {
                    await member.roles.add(role);
                    console.log(`Assigned role '${newRoleName}' to user ${member.displayName} (${member.id}).`);
                } catch (error) {
                    console.error(`Failed to assign role '${newRoleName}' to ${member.displayName} - ${error}`);
                }
            } else {
                console.log(`New role '${newRoleName}' not found in the guild.`);
            }
        } else {
            console.log(`No mapped role found for '${oldRoleName}' in ROLE_MAPPING.`);
        }
    }
}

(async () => {
    const commands = [
        new SlashCommandBuilder()
            .setName('update')
            .setDescription('Update roles for all members.')
            .toJSON()
    ];

    const rest = new REST({ version: '10' }).setToken(BOT_TOKEN);

    try {
        console.log('Registering slash commands...');
        await rest.put(
            Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID),
            { body: commands }
        );
        console.log('Slash commands registered successfully.');
    } catch (error) {
        console.error('Error registering commands:', error);
    }
})();

client.login(BOT_TOKEN);

module.exports = client;
